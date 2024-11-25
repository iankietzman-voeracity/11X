package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	// "log/slog"
	"net/http"
	"net/http/httputil"
	"strconv"
	levenshtein "github.com/texttheater/golang-levenshtein/levenshtein"
	// "reflect"
	// "strings"
)

type APIServer struct {
	addr string
}

type LevenshteinRequest struct {
    TargetSequence string 	`json:"target_sequence"`
	Read string				`json:"read_sequence"`
}

type Person struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func SimpleLogger(w http.ResponseWriter, r *http.Request) {
	dump, err := httputil.DumpRequest(r, true)
	if err != nil {
		http.Error(w, fmt.Sprint(err), http.StatusInternalServerError)
		return
	}
	log.Printf("%q", dump)
}

func BuildAPIServer(addr string) *APIServer {
	return &APIServer{
		addr: addr,
	}
}

func (s *APIServer) Run() error {
	router := http.NewServeMux()

	router.HandleFunc("GET /ping", func(w http.ResponseWriter, r *http.Request) {
		SimpleLogger(w, r)
		w.Write([]byte("pong"))
	})

	router.HandleFunc("GET /levenshtein", func(w http.ResponseWriter, r *http.Request) {
		SimpleLogger(w, r)
		w.Write([]byte("GOT"))
	})

	router.HandleFunc("POST /levenshtein", func(w http.ResponseWriter, r *http.Request) {
		SimpleLogger(w, r)
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			panic(err)
		}
		var sequence LevenshteinRequest
		err2 := json.Unmarshal(body, &sequence)
		if err2 != nil {
			panic(err2)
		}
		distance := levenshtein.DistanceForStrings([]rune(sequence.Read), []rune(sequence.TargetSequence), levenshtein.DefaultOptions)
		w.Write([]byte(strconv.Itoa(distance)))
	})

	server := http.Server{
		Addr: s.addr,
		Handler: router,
	}
	
	log.Printf("Server started %s", s.addr)

	return server.ListenAndServe()
}

