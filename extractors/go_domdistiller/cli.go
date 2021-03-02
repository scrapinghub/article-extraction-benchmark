package main

import (
	"fmt"
	"os"

	distiller "github.com/markusmobius/go-domdistiller"
)

func main() {
	if len(os.Args) < 2 {
		panic("Input file not provided in args")
	}
	if len(os.Args) > 2 {
		panic("Args accept only one argument")
	}
	input := os.Args[1]

	opts := &distiller.Options{
		ExtractTextOnly: true,
		SkipPagination: true,
	}

	article, err := distiller.ApplyForFile(input, opts)
	if err != nil {
		panic(err)
	}

	fmt.Print(article.HTML)
}
