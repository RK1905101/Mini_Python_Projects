from pypdf import PdfReader
from langchain.text_splitter import TextSplitter
from typing import List, Optional, Tuple
import re
import logging
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Configure logging
logger = logging.getLogger(__name__)

def setup_nltk() -> bool:
    """
    Set up NLTK dependencies safely
    
    Returns:
        bool: True if setup successful, False otherwise
    """
    required_packages = ['punkt', 'stopwords']
    try:
        for package in required_packages:
            try:
                nltk.data.find(f'tokenizers/{package}')
            except LookupError:
                logger.info(f"Downloading NLTK package: {package}")
                nltk.download(package, quiet=True)
        return True
    except Exception as e:
        logger.error(f"Failed to set up NLTK: {str(e)}")
        return False

# Initialize NLTK
if not setup_nltk():
    raise RuntimeError("Failed to initialize NLTK. Please check your internet connection and try again.")

class SemanticTextSplitter(TextSplitter):
    """Custom text splitter that tries to maintain semantic coherence"""
    
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        super().__init__(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self._chunk_size = chunk_size  # Using protected attribute as expected by TextSplitter
        self._chunk_overlap = chunk_overlap  # Using protected attribute as expected by TextSplitter
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            logger.warning(f"Failed to load stopwords, using minimal set: {str(e)}")
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to'])

    def split_documents(self, documents: List[str]) -> List[str]:
        """Implement the required abstract method"""
        return [chunk for doc in documents for chunk in self.split_text(doc)]

    def _get_sentence_similarity(self, sent1: str, sent2: str) -> float:
        """
        Calculate similarity between two sentences using word overlap
        
        Args:
            sent1: First sentence
            sent2: Second sentence
            
        Returns:
            float: Similarity score between 0 and 1
        """
        try:
            words1 = set(word.lower() for word in word_tokenize(sent1) if word.lower() not in self.stop_words)
            words2 = set(word.lower() for word in word_tokenize(sent2) if word.lower() not in self.stop_words)
            
            if not words1 or not words2:
                return 0.0
                
            overlap = len(words1.intersection(words2))
            similarity = overlap / (len(words1) + len(words2) - overlap)  # Jaccard similarity
            return similarity
        except Exception as e:
            logger.warning(f"Error calculating sentence similarity: {str(e)}")
            return 0.0
    
    def _find_best_split_point(self, text: str, target_length: int) -> int:
        """
        Find the best point to split the text based on semantic coherence
        
        Args:
            text: Text to split
            target_length: Target length for the split
            
        Returns:
            int: Best index to split the text
        """
        try:
            # Handle empty or short text
            if not text or len(text) <= target_length:
                return len(text)
            
            try:
                sentences = sent_tokenize(text)
            except Exception as e:
                logger.warning(f"Sentence tokenization failed: {str(e)}. Falling back to simple splits.")
                return min(target_length, len(text))
                
            if len(sentences) <= 1:
                return len(text)
                
            current_length = 0
            best_split_idx = 0
            min_coherence_loss = float('inf')
            
            # Track sentence boundaries for accurate split points
            sentence_boundaries = []
            current_pos = 0
            
            for sent in sentences:
                sent_start = text.find(sent, current_pos)
                if sent_start == -1:  # Fallback if exact match fails
                    sent_start = current_pos
                current_pos = sent_start + len(sent)
                sentence_boundaries.append((sent_start, current_pos))
            
            # Find best split point
            for i, (start, end) in enumerate(sentence_boundaries):
                if end > target_length:
                    # Calculate coherence metrics
                    if i > 0 and i < len(sentences) - 1:
                        prev_similarity = self._get_sentence_similarity(sentences[i-1], sentences[i])
                        next_similarity = self._get_sentence_similarity(sentences[i], sentences[i+1])
                        coherence_loss = prev_similarity + next_similarity
                        
                        if coherence_loss < min_coherence_loss:
                            min_coherence_loss = coherence_loss
                            best_split_idx = start
                    
                    # If no good split found, use current point
                    if min_coherence_loss == float('inf'):
                        best_split_idx = start
                    break
            
            # Ensure we return a valid split point
            if best_split_idx == 0:
                best_split_idx = target_length
                
            return best_split_idx
            
        except Exception as e:
            logger.error(f"Error finding split point: {str(e)}")
            return min(target_length, len(text))
    
    def split_text(self, text: str) -> List[str]:
        """Split text into semantically coherent chunks"""
        chunks = []
        current_text = text
        
        while len(current_text) > self._chunk_size:
            split_point = self._find_best_split_point(current_text, self._chunk_size)
            
            if split_point == len(current_text):
                chunks.append(current_text)
                break
                
            # Add chunk with overlap
            chunk = current_text[:split_point]
            chunks.append(chunk)
            
            # Keep overlap_size worth of text
            overlap_start = max(0, split_point - self._chunk_overlap)
            current_text = current_text[overlap_start:]
            
        if current_text:
            chunks.append(current_text)
            
        return chunks

class PDFProcessor:
    def __init__(self, chunk_size=2000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Using semantic-based splitting
        self.text_splitter = SemanticTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num} ---\n{page_text}"
            
            return text
        except Exception as e:
            print(f"Error extracting text: {str(e)}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove null bytes and normalize basic whitespace
        text = text.replace('\x00', '')
        
        # Fix common PDF artifacts
        text = re.sub(r'([^\n])\n([^\n])', r'\1 \2', text)  # Single newlines to spaces
        text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines to double
        
        # Remove excessive whitespace while preserving paragraph breaks
        text = re.sub(r' +', ' ', text)  # Multiple spaces to single
        text = re.sub(r'^ +| +$', '', text, flags=re.MULTILINE)  # Trim lines
        
        # Normalize paragraph breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()

    def extract_and_chunk_text(self, pdf_path: str) -> List[str]:
        """
        Extract and chunk text from PDF using semantic-aware splitting
        
        This method:
        1. Extracts text from PDF
        2. Cleans and normalizes the text
        3. Splits into semantic chunks while maintaining context coherence
        4. Post-processes chunks to ensure quality
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of semantically coherent text chunks
        """
        text = self.extract_text(pdf_path)
        
        if not text:
            return []
        
        # Clean and normalize text
        text = self.clean_text(text)
        
        # Split into semantic chunks
        raw_chunks = self.text_splitter.split_text(text)
        
        # Post-process chunks to ensure semantic integrity
        processed_chunks = []
        for chunk in raw_chunks:
            # Basic cleaning
            chunk = chunk.strip()
            
            # Skip if chunk is too small or meaningless
            if not chunk or len(chunk) < 100:  # Increased minimum size for semantic meaning
                continue
            
            # Ensure chunk ends at a proper sentence boundary if possible
            if not chunk.endswith(('.', '!', '?', ':"', '"', '"')):
                last_sentence_end = max(
                    chunk.rfind('.'), chunk.rfind('!'), chunk.rfind('?')
                )
                if last_sentence_end > len(chunk) * 0.8:  # Only trim if we keep most of the chunk
                    chunk = chunk[:last_sentence_end + 1]
            
            processed_chunks.append(chunk)
        
        return processed_chunks