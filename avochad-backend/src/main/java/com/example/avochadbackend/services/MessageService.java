package com.example.avochadbackend.services;


import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.avochadbackend.repo.MessageRepository;

import java.util.Date;
import java.util.List;

import com.example.avochadbackend.dto.MessageDTO;
import com.example.avochadbackend.models.Message;

@Service
@Transactional(readOnly = true)
public class MessageService {
    
    private final MessageRepository messageRepository;
    private final ModelMapper modelMapper;

    @Autowired
    public MessageService(MessageRepository messageRepository, ModelMapper modelMapper) {
        this.messageRepository = messageRepository;
        this.modelMapper = modelMapper;
    }

    public List<Message> findAll(){
        return this.messageRepository.findAll();
    }

    public Message findById(long id) {
        return this.messageRepository.findById(id).get();
    }


    public List<Message> findByChatId(long id) {
        return this.messageRepository.findByChatId(id);
    }


    @Transactional
    public void save(Message message) {

        message.setCreatedAt(new Date());
        message.setUpdatedAt(new Date());
        this.messageRepository.save(message);
    }

    @Transactional
    public void update(Message message) {
        message.setUpdatedAt(new Date());
        this.messageRepository.save(message);
    }


    public Message convertMessageDtoToMessage(MessageDTO messageDTO) {
        return modelMapper.map(messageDTO, Message.class);
    }
}
