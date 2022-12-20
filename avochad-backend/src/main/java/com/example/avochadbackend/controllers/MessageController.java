package com.example.avochadbackend.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.avochadbackend.dto.MessageDTO;
import com.example.avochadbackend.models.Message;
import com.example.avochadbackend.services.MessageService;
import com.example.avochadbackend.utility.exception.ErrorResponse;
import com.example.avochadbackend.utility.exception.messageExceptions.MessageNotCreatedException;
import com.example.avochadbackend.utility.exception.messageExceptions.MessageNotFoundException;

import net.bytebuddy.implementation.bind.MethodDelegationBinder.BindingResolver;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/messages")
public class MessageController {

    private final MessageService messageService;


    @Autowired
    public MessageController(MessageService messageService) {
        this.messageService = messageService;
    }

    @GetMapping("/")
    public ResponseEntity<List<Message>> findAll() {
        return new ResponseEntity<>(this.messageService.findAll(), HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Message> findById(long id) {
        
        Optional<Message> message = Optional.ofNullable(this.messageService.findById(id));

        if(message.isEmpty())
            throw new MessageNotFoundException("Message not found");

        return new ResponseEntity<>(this.messageService.findById(id), HttpStatus.OK);
    }

    @GetMapping("/chat/{id}")
    public ResponseEntity<List<Message>> findByChatId(long id) {
        return new ResponseEntity<>(this.messageService.findByChatId(id), HttpStatus.OK);
    }

    @PostMapping("/")
    public ResponseEntity<Message> save(@RequestBody MessageDTO messageDTO, BindingResult bindingResult) {
        Message message = this.messageService.convertMessageDtoToMessage(messageDTO);

        if(bindingResult.hasErrors()){
            StringBuilder errors = new StringBuilder();

            for(FieldError error : bindingResult.getFieldErrors())
                errors.append(error.getField() + " " + error.getDefaultMessage() + ";");
            
            throw new MessageNotCreatedException(errors.toString());
        }



        this.messageService.save(message);
        return new ResponseEntity<>(message, HttpStatus.OK);
    }

    @ExceptionHandler(MessageNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleMessageNotFoundException(MessageNotFoundException e) {
        return new ResponseEntity<>(new ErrorResponse(e.getMessage(), System.currentTimeMillis()), HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(MessageNotCreatedException.class)
    public ResponseEntity<ErrorResponse> handleMessageNotCreatedException(MessageNotCreatedException e) {
        return new ResponseEntity<>(new ErrorResponse(e.getMessage(), System.currentTimeMillis()), HttpStatus.BAD_REQUEST);
    }


}
