# Use official Golang image to build the application
FROM golang:1.20 AS builder

WORKDIR /app
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o go_router main.go


# Use a minimal base image to run the binary
FROM alpine:latest

WORKDIR /root/
COPY --from=builder /app/go_router .
EXPOSE 9000

# Run the Go application
CMD ["./go_router"]

