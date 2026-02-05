use std::env;
use std::io::{self, Read};

fn normalize(s: &str) -> String {
    s.replace('\u{00ad}', "").replace("\r\n", "\n")
}

fn html_to_text(html: &str) -> String {
    html2text::from_read(html.as_bytes(), 80).unwrap_or_default()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args().skip(1);
    let backend = args.next().ok_or("missing backend")?;
    let mut url: Option<String> = None;
    while let Some(arg) = args.next() {
        if arg == "--url" {
            url = args.next();
        } else {
            return Err(format!("unknown argument: {arg}").into());
        }
    }

    let mut html = String::new();
    io::stdin().read_to_string(&mut html)?;
    let url = url.unwrap_or_else(|| "https://example.com/".to_string());

    let output = match backend.as_str() {
        "august" => normalize(&august::convert(&html, 80)),
        "fast_html2md" => {
            let md = fast_html2md::rewrite_html(&html, false);
            normalize(&md)
        }
        "htmd" => normalize(&htmd::convert(&html).unwrap_or_default()),
        "html2md-rs" => {
            let parsed = html2md_rs::to_md::safe_from_html_to_md(html.clone()).unwrap_or_default();
            normalize(&parsed)
        }
        "html2text" => normalize(&html_to_text(&html)),
        "llm_readability" => {
            let mut reader = html.as_bytes();
            let parsed_url = url::Url::parse(&url)?;
            let product = llm_readability::extractor::extract(&mut reader, &parsed_url)?;
            normalize(&product.text)
        }
        "mdka" => normalize(&mdka::from_html(&html)),
        "nanohtml2text" => normalize(&nanohtml2text::html2text(&html)),
        "boilerpipe" => {
            let doc = boilerpipe::parse_document(&html);
            normalize(doc.content().as_ref())
        }
        "readability" => {
            let mut reader = html.as_bytes();
            let parsed_url = url::Url::parse(&url)?;
            let readable = readability::extractor::extract(&mut reader, &parsed_url)?;
            normalize(&readable.text)
        }
        "readabilityrs" => {
            let article = readabilityrs::Readability::new(&html, Some(&url), None)?
                .parse()
                .ok_or("readabilityrs: no article found")?;
            normalize(&html_to_text(
                article.content.as_deref().unwrap_or_default(),
            ))
        }
        "dom_smoothie" => {
            let mut readability = dom_smoothie::Readability::new(html.clone(), Some(&url), None)?;
            let article = readability.parse()?;
            normalize(&html_to_text(&article.content))
        }
        "readable-readability" => {
            let mut readability = readable_readability::Readability::new();
            if let Ok(parsed) = url::Url::parse(&url) {
                readability.base_url(parsed);
            }
            let (node, _meta) = readability.parse(&html);
            normalize(&node.text_contents())
        }
        "rs_trafilatura" => {
            let result = rs_trafilatura::extract(&html)?;
            normalize(&result.content_text)
        }
        _ => {
            eprintln!("unknown backend: {backend}");
            String::new()
        }
    };

    print!("{output}");
    Ok(())
}
