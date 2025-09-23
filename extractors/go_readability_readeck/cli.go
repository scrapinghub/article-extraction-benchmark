package main

import (
	"fmt"
	"net/url"
	"os"

	readability "codeberg.org/readeck/go-readability"
	"golang.org/x/net/html"
)

func main() {
	doc, err := html.Parse(os.Stdin)
	if err != nil {
		panic(err)
	}

	u, _ := url.Parse("https://fake-url.com")

	parser := readability.NewParser()
	article, err := parser.ParseAndMutate(doc, u)
	if err != nil {
		panic(err)
	}

	fmt.Print(article.TextContent)
}
