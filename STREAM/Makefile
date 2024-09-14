# Compiler and flags
CC = gcc
CFLAGS = -O3 

# Target executable
TARGET = stream

# Source file
SRC = stream.c

# Default rule to build the target
all: $(TARGET)

# Rule to build the executable
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)


# Rule for cleaning up the compiled files
clean:
	rm -f $(TARGET)
