from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import logging
import torch
from typing import List, Tuple, Optional, Dict, Any
import gc
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelNotFoundError(Exception):
    """Raised when a model cannot be loaded."""
    pass

class LLMError(Exception):
    """Base class for LLM-related errors."""
    pass

def clean_gpu_memory():
    """Clean up GPU memory if available"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()

class LLMHandler:
    def __init__(self, model_name="google/flan-t5-base", fallback_models: List[str] = None):
        """
        Initialize the LLM
        Using T5 models which are encoder-decoder models (not causal LMs)
        Options:
        - "google/flan-t5-small" (80M parameters)
        - "google/flan-t5-base" (250M parameters)
        - "google/flan-t5-large" (780M parameters)
        
        Args:
            model_name: Name of the primary model to load
            fallback_models: List of backup models to try if primary fails
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name
        self.fallback_models = fallback_models or ["google/flan-t5-small"]
        self.max_retries = 3
        self.model = None
        self.tokenizer = None
        
        try:
            self._initialize_model(model_name)
        except Exception as e:
            logger.error(f"Failed to load primary model {model_name}: {str(e)}")
            self._try_fallback_models()

    def _initialize_model(self, model_name: str) -> None:
        """Initialize the model and tokenizer"""
        try:
            logger.info(f"Loading model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            
            # Set padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name, 
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
                
            logger.info(f"Successfully loaded model: {model_name}")
        except Exception as e:
            raise ModelNotFoundError(f"Failed to load model {model_name}: {str(e)}")

    def _try_fallback_models(self) -> None:
        """Try loading fallback models if primary fails"""
        for model_name in self.fallback_models:
            try:
                self._initialize_model(model_name)
                logger.info(f"Successfully loaded fallback model: {model_name}")
                return
            except Exception as e:
                logger.error(f"Failed to load fallback model {model_name}: {str(e)}")
        
        raise ModelNotFoundError("Failed to load any models, including fallbacks")

    def _cleanup(self) -> None:
        """Clean up resources"""
        clean_gpu_memory()

    def _create_prompt(self, question: str, context: str, require_detail: bool = False) -> str:
        """
        Create an optimized prompt based on the type of question
        """
        base_prompt = f"""You are a helpful AI assistant tasked with answering questions based on provided context.
Always provide detailed, multi-sentence answers that thoroughly explain the topic.
Never give one-word or short answers - explain your reasoning and provide context.

Based on the following context from a document, provide a comprehensive and detailed answer to the question.
If the answer cannot be found in the context, clearly state that and explain why.
Use only information from the context - do not make assumptions or add external information.
            
Context:
{context[:3000]}

Question: {question}

Requirements for your answer:
1. ALWAYS write at least 3-4 complete sentences
2. Include specific examples, numbers, or quotes from the context to support your answer
3. Explain any technical terms or concepts mentioned
4. Structure your answer logically with clear transitions
5. If relevant, mention relationships between different ideas in the context
6. Begin with a clear topic sentence that directly addresses the question
7. End with a concluding statement that summarizes the key points"""

        if require_detail:
            base_prompt += """
Additional requirements for detailed response:
8. Analyze multiple aspects or perspectives of the topic
9. Compare and contrast relevant information from different parts of the context
10. Provide step-by-step explanations where applicable
11. Discuss implications or consequences if relevant
12. Highlight any limitations or uncertainties in the information"""

        base_prompt += "\n\nDetailed Answer:"
        return base_prompt

    def _process_answer(self, answer: str) -> str:
        """Clean and process the generated answer"""
        def remove_duplicates(text: str) -> str:
            """Remove duplicate sentences while preserving order and context"""
            sentences = re.split(r'(?<=[.!?])\s+', text)
            seen = set()
            unique = []
            for s in sentences:
                s_clean = ' '.join(s.strip().split())
                # Keep sentences that add new information
                if (s_clean and s_clean.lower() not in seen and 
                    len(s_clean.split()) > 3):  # Minimum word count per sentence
                    seen.add(s_clean.lower())
                    unique.append(s_clean)
            return ' '.join(unique)

        def ensure_complete_sentences(text: str) -> str:
            """Ensure the text ends with complete sentences"""
            # Find the last sentence boundary
            last_boundary = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
            if last_boundary > 0 and last_boundary < len(text) - 1:
                # Keep the text up to the last complete sentence
                text = text[:last_boundary + 1]
            return text

        def expand_abbreviations(text: str) -> str:
            """Expand common abbreviations for clarity"""
            abbreviations = {
                r'\be\.g\.\s': 'for example, ',
                r'\bi\.e\.\s': 'that is, ',
                r'\betc\.\s': 'and so forth, ',
                r'\bvs\.\s': 'versus ',
                r'\bfig\.\s': 'figure ',
                r'\bexp\.\s': 'experiment ',
                r'\bref\.\s': 'reference '
            }
            for abbr, expanded in abbreviations.items():
                text = re.sub(abbr, expanded, text)
            return text

        try:
            # Basic cleanup
            answer = answer.strip()
            answer = re.sub(r'\s+', ' ', answer)  # Normalize whitespace
            
            # Remove common prefixes
            prefixes = [
                "Here's the answer:", 
                "Based on the context:", 
                "The answer is:",
                "According to the context,",
                "Based on the provided information,"
            ]
            for prefix in prefixes:
                if answer.lower().startswith(prefix.lower()):
                    answer = answer[len(prefix):].strip()

            # Process the answer
            answer = expand_abbreviations(answer)
            answer = remove_duplicates(answer)
            answer = ensure_complete_sentences(answer)

            # Ensure minimum length and completeness
            if len(answer.split()) < 20:  # Minimum 20 words
                logger.warning("Answer too short, regenerating...")
                raise ValueError("Answer too short")

            return answer

        except Exception as e:
            logger.error(f"Error processing answer: {str(e)}")
            if len(answer.split()) < 20:
                return "I apologize, but I need to generate a more detailed answer. Please try asking the question again."
            return answer

    def generate_answer(self, question: str, context: List[Tuple[str, float]], require_detail: bool = False) -> str:
        """
        Generate an answer based on the question and context
        
        Args:
            question: User's question
            context: List of (text, relevance_score) tuples
            require_detail: Whether to generate a more detailed answer
        
        Returns:
            str: Generated answer
            
        Raises:
            LLMError: If answer generation fails
        """
        try:
            # Sort and combine context
            sorted_context = sorted(context, key=lambda x: x[1], reverse=True)
            combined_context = "\n".join(text for text, _ in sorted_context)
            
            # Create optimized prompt
            prompt = self._create_prompt(question, combined_context, require_detail)
            
            # Generation parameters optimized for detailed responses
            gen_params = {
                "max_length": 1024 if require_detail else 768,  # Increased max length
                "min_length": 100,  # Enforce minimum response length
                "num_beams": 5,  # Increased beam search
                "temperature": 0.85 if require_detail else 0.75,  # Slightly increased creativity
                "do_sample": True,
                "top_p": 0.92,  # Slightly reduced to focus on more likely tokens
                "no_repeat_ngram_size": 3,
                "length_penalty": 1.2,  # Encourage longer responses
                "early_stopping": False,  # Let it generate full-length responses
                "repetition_penalty": 1.2  # Discourage repetitive text
            }
            
            # Generate with retry mechanism
            for attempt in range(self.max_retries):
                try:
                    inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024)
                    inputs = inputs.to(self.device)
                    
                    outputs = self.model.generate(
                        inputs,
                        pad_token_id=self.tokenizer.pad_token_id,
                        **gen_params
                    )
                    
                    answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                    answer = self._process_answer(answer)
                    
                    # Cleanup
                    del inputs, outputs
                    self._cleanup()
                    
                    return answer
                    
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == self.max_retries - 1:
                        raise
                    self._cleanup()
                    
        except Exception as e:
            logger.error(f"Failed to generate answer: {str(e)}")
            raise LLMError(f"Failed to generate answer: {str(e)}")

    def __del__(self):
        """Cleanup when the object is destroyed"""
        self._cleanup()


class LLMHandlerT5:
    """Lightweight alternative implementation using T5 models"""
    
    def __init__(self, model_name="google/flan-t5-base"):
        """
        Initialize a lightweight T5-based handler (better for CPU-only systems)
        
        Args:
            model_name: Name of the T5 model to use
                Options: 
                - "google/flan-t5-small" (80M parameters)
                - "google/flan-t5-base" (250M parameters)
                - "google/flan-t5-large" (780M parameters)
        """
        from transformers import T5ForConditionalGeneration, T5Tokenizer
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing T5 handler with model: {model_name} on {self.device}")
        
        try:
            self.tokenizer = T5Tokenizer.from_pretrained(model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            self.model = self.model.to(self.device)
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
        except Exception as e:
            raise ModelNotFoundError(f"Failed to initialize T5 model: {str(e)}")
    
    def generate_answer(self, question: str, context: List[Tuple[str, float]]) -> str:
        """
        Generate an answer using the T5 model
        
        Args:
            question: User's question
            context: List of (text, relevance_score) tuples
        
        Returns:
            str: Generated answer
        """
        try:
            # Process context
            max_chunks = 5
            context_text = "\n".join(
                text for text, _ in sorted(context, key=lambda x: x[1], reverse=True)[:max_chunks]
            )
            
            # Create prompt
            prompt = f"""Answer the question based on the context. Be clear and concise.
            If the answer is not in the context, say so.
            
            Context: {context_text[:2000]}
            
            Question: {question}
            
            Answer:"""
            
            # Generate answer
            inputs = self.tokenizer.encode(
                prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True
            ).to(self.device)
            
            outputs = self.model.generate(
                inputs,
                max_length=150,
                min_length=20,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                num_beams=3,
                no_repeat_ngram_size=2,
                early_stopping=True
            )
            
            answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up
            del inputs, outputs
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Process answer
            answer = answer.strip()
            if answer.lower().startswith("answer:"):
                answer = answer[7:].strip()
            
            return answer
            
        except Exception as e:
            logger.error(f"Error generating T5 answer: {str(e)}")
            return f"Error generating answer: {str(e)}"
    
    def __del__(self):
        """Cleanup when the object is destroyed"""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            gc.collect()