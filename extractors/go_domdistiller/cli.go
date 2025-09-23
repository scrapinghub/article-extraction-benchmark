package main

import (
	"fmt"
	"os"

	distiller "github.com/markusmobius/go-domdistiller"
	"golang.org/x/net/html"
)

func main() {
	doc, err := html.Parse(os.Stdin)
	if err != nil {
		panic(err)
	}

	article, err := distiller.Apply(doc, &distiller.Options{
		SkipPagination: true,
	})
	if err != nil {
		panic(err)
	}

	fmt.Print(article.Text)
}
