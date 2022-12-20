package com.example.avochadbackend.dto;

import com.example.avochadbackend.utility.enums.MessageType;

public class MessageDTO {
    
    private MessageType messageType;
    private String text;
    private Long userId;
    private Long chatId;
    private Long fileId;

    public MessageDTO() {}

    public MessageDTO(MessageType messageType, String text, Long userId, Long chatId, Long fileId) {
        this.messageType = messageType;
        this.text = text;
        this.userId = userId;
        this.chatId = chatId;
        this.fileId = fileId;
    }

    public MessageType getMessageType() {
        return messageType;
    }

    public String getText() {
        return text;
    }

    public Long getUserId() {
        return userId;
    }

    public Long getChatId() {
        return chatId;
    }

    public Long getFileId() {
        return fileId;
    }

    public void setMessageType(MessageType messageType) {
        this.messageType = messageType;
    }

    public void setText(String text) {
        this.text = text;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public void setChatId(Long chatId) {
        this.chatId = chatId;
    }

    public void setFileId(Long fileId) {
        this.fileId = fileId;
    }


}
