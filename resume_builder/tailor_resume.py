"""Stateless resume tailoring: one API call, no history, raw Markdown out."""
import os
import sys
import time
from pathlib import Path

import anthropic

HERE = Path(__file__).resolve().parent
MODEL = os.environ.get("RESUME_MODEL", "claude-sonnet-5-5")

# Instructions live in `system` (short, fixed). Output-only directive saves tokens.
SYSTEM = (
    "You tailor resumes. Output ONLY the final tailored resume in Markdown. "
    "No preamble, no commentary, no code fences, no closing remarks. "
    "Rules: use only facts present in the master resume (never invent employers, "
    "titles, dates, metrics or skills); reorder and reword to mirror the job "
    "description's keywords; lead with the most relevant experience; cut irrelevant "
    "items; keep bullets concise and quantified where the source has numbers; "
    "target one page."
)


def read(name: str) -> str:
    text = (HERE / name).read_text(encoding="utf-8").strip()
    if not text:
        sys.exit(f"Error: {name} is empty. Paste your content into it first.")
    return text


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Error: ANTHROPIC_API_KEY is not set in your environment.")

    resume = read("master_resume.txt")
    job = read("job_description.txt")

    client = anthropic.Anthropic(api_key=api_key)
    start = time.time()
    response = client.messages.create(
        model=MODEL,
        max_tokens=3000,  # hard cap on output spend; a one-page resume is ~1k tokens
        system=SYSTEM,
        output_config={"effort": "low"},  # minimal reasoning overhead
        messages=[{
            "role": "user",
            "content": f"<master_resume>\n{resume}\n</master_resume>\n\n"
                       f"<job_description>\n{job}\n</job_description>",
        }],
    )

    if response.stop_reason == "refusal":
        sys.exit("Error: request was declined by the model.")
    text = "".join(b.text for b in response.content if b.type == "text").strip()
    if not text:
        sys.exit("Error: empty response.")

    (HERE / "tailored_resume.md").write_text(text + "\n", encoding="utf-8")
    u = response.usage
    note = " (hit max_tokens, output truncated)" if response.stop_reason == "max_tokens" else ""
    print(f"Done in {time.time() - start:.1f}s | {u.input_tokens} in / {u.output_tokens} out tokens"
          f" | saved tailored_resume.md{note}")


if __name__ == "__main__":
    main()
