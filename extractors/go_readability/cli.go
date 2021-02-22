package main

import (
	"fmt"
	"os"

	readability "github.com/go-shiori/go-readability"
)

func main() {
	if len(os.Args) < 2 {
		panic("Input file not provided in args")
	}
	if len(os.Args) > 2 {
		panic("Args accept only one argument")
	}
	input := os.Args[1]

	fSrc, err := os.Open(input)
	defer fSrc.Close()
	if err != nil {
		panic(err)
	}

	article, err := readability.FromReader(fSrc, "https://fake-url.com")
	if err != nil {
		panic(err)
	}

	fmt.Print(article.TextContent)
}
