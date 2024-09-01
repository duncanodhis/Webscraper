from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

# Function to load HTML documents from a list of URLs
def load_html_documents(urls):
    loader = AsyncHtmlLoader(urls)
    return loader.load()

# Function to transform HTML documents to plain text
def transform_html_to_text(docs):
    html2text = Html2TextTransformer()
    return html2text.transform_documents(docs)

# Function to save transformed documents to a text file
def save_documents_to_file(docs_transformed, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(f"{doc.page_content}\n" for doc in docs_transformed)

# Main function to perform the complete pipeline
def main(urls, output_file):
    docs = load_html_documents(urls)
    docs_transformed = transform_html_to_text(docs)
    save_documents_to_file(docs_transformed, output_file)

# Execute the program
if __name__ == "__main__":
    urls = ["https://www.espn.com", "https://lilianweng.github.io/posts/2023-06-23-agent/"]
    main(urls, 'output.txt')
