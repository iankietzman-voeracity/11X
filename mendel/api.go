package main

import "log"
import "net/http"

type APIServer struct {
	addr string
}

func BuildAPIServer(addr string) *APIServer {
	return &APIServer{
		addr: addr,
	}
}

func (s *APIServer) Run() error {
	router := http.NewServeMux()

	router.HandleFunc("GET /levenshtein", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("testing three"))
	})

	router.HandleFunc("POST /levenshtein", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("testing"))
	})

	server := http.Server{
		Addr: s.addr,
		Handler: router,
	}

	log.Printf("Server started %s", s.addr)

	return server.ListenAndServe()
}

