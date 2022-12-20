package com.example.avochadbackend.models;

import com.example.avochadbackend.utility.enums.MessageType;
import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnore;

import java.util.Date;
import java.util.HashSet;
import java.util.Objects;

import javax.persistence.*;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

@Entity
@Table(name = "message")
public class Message {

    @Column(name = "id")
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "type")
    @NotNull
    private MessageType messageType;

    @Column(name = "text")
    @NotEmpty(message = "Text is mandatory")
    private String text;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    @JsonBackReference
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "chat_id")
    @JsonIgnore
    private Chat chat;

    @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "file_id")
    @JsonIgnore
    private File file;

    @Column(name = "created_at")
    @Temporal(TemporalType.TIMESTAMP)
    private Date createdAt;

    @Column(name = "updated_at")
    @Temporal(TemporalType.TIMESTAMP)
    private Date updatedAt;

    public Message() {}

    public Message(MessageType messageType, String text, Date createdAt, Date updatedAt, User user, Chat chat) {
        this.messageType = messageType;
        this.text = text;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.user = user;
        this.chat = chat;
    }

    public Long getId() {
        return id;
    }

    public MessageType getMessageType() {
        return messageType;
    }

    public String getText() {
        return text;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public Date getUpdatedAt() {
        return updatedAt;
    }

    public User getUser() {
        return user;
    }

    public Chat getChat() {
        return chat;
    }

    public void setMessageType(MessageType messageType) {
        this.messageType = messageType;
    }

    public void setText(String text) {
        this.text = text;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public void setChat(Chat chat) {
        this.chat = chat;
    }

    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || !(o instanceof Message)) return false;
        Message message = (Message) o;

        return id.equals(message.id) &&
                messageType == message.messageType &&
                text.equals(message.text) &&
                createdAt.equals(message.createdAt) &&
                updatedAt.equals(message.updatedAt) &&
                user.equals(message.user) &&
                chat.equals(message.chat);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, messageType, text, createdAt, updatedAt, user, chat);
    }


    @Override
    public String toString() {
        return "Message{" +
                "id=" + id +
                ", messageType=" + messageType +
                ", text='" + text + '\'' +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                ", user=" + user +
                ", chat=" + chat +
                '}';
    }



}
