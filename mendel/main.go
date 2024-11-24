package main

func main() {
	server := BuildAPIServer(":8443")
	server.Run()
}