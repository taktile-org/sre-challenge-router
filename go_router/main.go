package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type BackendResponse struct {
	Message string `json:"message"`
}

func fetchBackend(url string) (BackendResponse, error) {
	resp, err := http.Get(url)
	if err != nil {
		return BackendResponse{}, fmt.Errorf("error contacting %s: %v", url, err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return BackendResponse{}, fmt.Errorf("error reading response from %s: %v", url, err)
	}

	var result BackendResponse
	if err := json.Unmarshal(body, &result); err != nil {
		return BackendResponse{}, fmt.Errorf("invalid response from %s: %v", url, err)
	}

	return result, nil
}

func handler(w http.ResponseWriter, r *http.Request) {
	backends := []string{
		"http://backend_good:9000/",
		"http://backend_average:9000/",
		"http://backend_faulty:9000/",
	}

	backend := backends[0]

	backend1Response, err := fetchBackend(backend)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(backend1Response.Message)
}

func main() {
	http.HandleFunc("/", handler)
	fmt.Println("Go router running on port 9000")
	if err := http.ListenAndServe(":9000", nil); err != nil {
		fmt.Printf("Error starting server: %v\n", err)
	} 
}
