#! /usr/bin/env python3
import argparse
import pathlib
import os
import copy
from PyPDF2 import PdfReader, PdfWriter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Combine generated labels with a scan/template to check alignment."
    )
    parser.add_argument(
        "-t",
        "--template",
        type=pathlib.Path,
        help="Path to the template file (e.g., a scan or a template image).",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--labels",
        type=pathlib.Path,
        help="Path to the generatel labels PDF.",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("alignment_check.pdf"),
        help="Path to save the output PDF with alignment check.",
        required=False,
    )
    return parser.parse_args()


def check_template_length(template_path):
    """Check the length of the template PDF."""
    if not template_path.exists():
        raise FileNotFoundError(f"Template file {template_path} does not exist.")
    
    reader = PdfReader(template_path)
    if len(reader.pages) != 1:
        raise ValueError(f"Template file {template_path} should contain exactly one page.")

def combine_pdfs(template_path, labels_path, output_path):
    """Combine the template and labels PDFs into a single output PDF."""
    template_reader = PdfReader(template_path)
    labels_reader = PdfReader(labels_path)
    writer = PdfWriter()
    
    if len(template_reader.pages) != 1:
        raise ValueError("Template PDF should contain exactly one page.")
    
    for i in range(len(labels_reader.pages)):
        content_page = copy.deepcopy(template_reader.pages[0])
        content_page.merge_page(labels_reader.pages[i])
        writer.add_page(content_page)

    with open(output_path, "wb") as output_file:
        writer.write(output_file)

def main():
    args = parse_args()

    # First we just make sure that the template and labels files exist
    check_template_length(args.template)
    if not args.labels.exists():
        raise FileNotFoundError(f"Labels file {args.labels} does not exist.")
    
    # make sure the output path exists and is writable
    if not args.output.parent.exists():
        raise FileNotFoundError(f"Output directory {args.output.parent} does not exist.")
    if not args.output.parent.is_dir():
        raise NotADirectoryError(f"Output path {args.output.parent} is not a directory.")
    if not os.access(args.output.parent, os.W_OK):
        raise PermissionError(f"Output directory {args.output.parent} is not writable.")
    
    # Now we can combine the PDFs
    combine_pdfs(args.template, args.labels, args.output)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)