# Website Summarizer CLI

A **command-line interface (CLI) tool** that generates a beautiful, structured summary of any website using **Google's Generative AI** (Gemini). Summaries are saved in Markdown format for easy reading and sharing.

---

## Features

- Fetches text content from any URL.
- Generates a structured summary in Markdown using **Google Gemini AI**.
- Displays the summary in the terminal with a typewriter effect.
- Saves the summary as a `.md` file in a `summaries/` folder.
- Easy-to-use interactive CLI.

---

## Demo

```bash
$ python main.py
Hello I am your chatbot. To exit write Quit
Enter URL or quit to exit: https://example.com
<---Summary--->
✅ Summary saved to 'summaries/example_com_summary.md'
