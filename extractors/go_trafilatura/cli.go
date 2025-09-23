package main

import (
	"fmt"
	"os"

	"github.com/markusmobius/go-trafilatura"
	"golang.org/x/net/html"
)

func main() {
	doc, err := html.Parse(os.Stdin)
	if err != nil {
		panic(err)
	}

	result, err := trafilatura.ExtractDocument(doc, trafilatura.Options{
		EnableFallback: true,
	})
	if err != nil {
		panic(err)
	}
	_, err = fmt.Println(result.ContentText)
	if err != nil {
		panic(err)
	}
}
