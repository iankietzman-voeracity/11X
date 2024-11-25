package main

import (
	// "fmt"
	"time"
	"strings"
	"log"
	"os"
)

func main() {
	currentTime := time.Now()
	file, err := os.OpenFile("./logs/" + strings.ReplaceAll((currentTime.Format("2006 1 2")), " ", "_") + ".log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
    if err != nil {
        log.Fatal(err)
    }
    log.SetOutput(file)

	server := BuildAPIServer(":8443")
	server.Run()
}