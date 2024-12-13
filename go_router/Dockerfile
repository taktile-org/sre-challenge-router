# Use official Golang image to build the application
FROM golang:1.23

WORKDIR /app
COPY main.go .
RUN go install github.com/mitranim/gow@latest

EXPOSE 9000

# Run the Go application
CMD ["gow", "run", "main.go"]

