package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"sync"
	"time"
)

type BackendResponse struct {
	Message string `json:"message"`
}

var (
	counter     int
	requestHits = make(map[string]int)
	mu          sync.Mutex
)

func fetchBackend(backendURL, path string) (BackendResponse, error) {
	fullURL := urlJoin(backendURL, path)
	resp, err := http.Get(fullURL)
	if err != nil {
		return BackendResponse{}, fmt.Errorf("error contacting %s: %v", fullURL, err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return BackendResponse{}, fmt.Errorf("error reading response from %s: %v", fullURL, err)
	}

	var result BackendResponse
	if err := json.Unmarshal(body, &result); err != nil {
		return BackendResponse{}, fmt.Errorf("invalid response from %s: %v", fullURL, err)
	}

	return result, nil
}

func urlJoin(base, path string) string {
	u, err := url.Parse(base)
	if err != nil {
		return base
	}
	u.Path = url.JoinPath(u.Path, path)
	return u.String()
}

func handler(w http.ResponseWriter, r *http.Request) {
	backends := []string{
		"http://backend_good:9000/",
		"http://backend_average:9000/",
		"http://backend_faulty:9000/",
	}

	mu.Lock()
	backend := backends[counter%len(backends)]
	counter++
	requestHits[backend]++
	mu.Unlock()

	startTime := time.Now()
	backendResponse, err := fetchBackend(backend, r.URL.Path)
	requestTime := time.Since(startTime)

	fmt.Printf("Request time: %v seconds from %s\n", requestTime.Seconds(), backend)

	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(backendResponse.Message)
}

func main() {
	http.HandleFunc("/", handler)
	fmt.Println("Go router running on port 9000")
	if err := http.ListenAndServe(":9000", nil); err != nil {
		fmt.Printf("Error starting server: %v\n", err)
	}
}
