IMAGE_NAME=text_file_converter
CONTAINER_NAME=text_file_converter_container

build:
	docker build -t $(IMAGE_NAME) .

run:
	# Stop and remove the existing container if it exists
	docker rm -f $(CONTAINER_NAME) || true
	# Run a new container with the specified name and volume mappings
	docker run --name $(CONTAINER_NAME) \
		-v $(PWD)/input_files:/app/input_files \
		-v $(PWD)/output_files:/app/output_files \
		$(IMAGE_NAME)

clean:
	docker rm -f $(CONTAINER_NAME) || true
	docker rmi -f $(IMAGE_NAME) || true
