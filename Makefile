CC = clang++

CFLAGS = -g -Wall

LFLAGS = -lcs50

TARGET = main

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).cpp $(LFLAGS)

