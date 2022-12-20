package com.example.avochadbackend.utility.exception.messageExceptions;

public class MessageNotFoundException extends RuntimeException {
    
    public MessageNotFoundException(String message) {
        super(message);
    }
}
