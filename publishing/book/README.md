# Student learning book

Title: Distributed Systems

Lecturer: assoc. prof. Nikola Tankovic, PhD

Faculty: Faculty of Informatics, Juraj Dobrila University of Pula

## Assembly order

The proposed sequence is in `../../COURSE.md`. Draft samples are currently included to test assembly. Maintain `book.chapters` in `_quarto.yml`. Paths are relative to the repository root in the temporary build workspace. Keep `index.qmd` first, followed by reviewed `lectures/NN-short-topic/chapter.qmd` files. Do not include the lecture template.

## Publishing

Use `just book` for the complete PDF and `just lecture NN-short-topic` for a lecture PDF. Run commands from the repository root. Quarto uses the existing XeLaTeX installation. Outputs go to `output/book/` and `output/lectures/`.

`index.qmd` contains book front matter; `lecture.yml` supplies standalone lecture PDF defaults. See the root `README.md` for setup and workflow.
