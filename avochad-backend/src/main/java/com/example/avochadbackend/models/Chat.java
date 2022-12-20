package com.example.avochadbackend.models;

import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

import com.example.avochadbackend.utility.enums.ChatType;
import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;

import java.util.Date;
import java.util.Objects;
import java.util.List;

@Entity
@Table(name = "chat")
public class Chat {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "title")
    @Size(min = 2, max = 254, message = "Title must be between 2 and 254 characters")
    private String title;

    @Column(name = "type")
    @NotNull(message = "Type is mandatory")
    @Enumerated(EnumType.ORDINAL)
    private ChatType type;

    @ManyToMany(cascade = CascadeType.ALL)
    @JoinTable(
        name = "chat_user",
        joinColumns = @JoinColumn(name = "chat_id"),
        inverseJoinColumns = @JoinColumn(name = "user_id")
    )
    @JsonManagedReference
    private List<User> users;

    @OneToOne(cascade = CascadeType.ALL)
    @JsonBackReference
    private Channel channel;

    @Column(name = "created_at")
    @Temporal(TemporalType.TIMESTAMP)
    private Date createdAt;

    @Column(name = "updated_at")
    @Temporal(TemporalType.TIMESTAMP)
    private Date updatedAt;

    

    public Chat() {}

    public Chat(String title, ChatType type, Date createdAt, Date updatedAt, Channel channel) {
        this.title = title;
        this.type = type;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.channel = channel;
    }
    
    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public ChatType getType() {
        return type;
    }

    public Date getCreatedAt() {
        return createdAt;
    }

    public Date getUpdatedAt() {
        return updatedAt;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setType(ChatType type) {
        this.type = type;
    }

    public void setCreatedAt(Date createdAt) {
        this.createdAt = createdAt;
    }

    public void setUpdatedAt(Date updatedAt) {
        this.updatedAt = updatedAt;
    }

    public List<User> getUsers() {
        return users;
    }

    public void setUsers(List<User> users) {
        this.users = users;
    }

    public Channel getChannel() {
        return channel;
    }

    public void setChannel(Channel channel) {
        this.channel = channel;
    }

    

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || !(o instanceof Chat)) return false;
        Chat chat = (Chat) o;
        return Objects.equals(id, chat.id) && Objects.equals(title, chat.title) && type == chat.type && Objects.equals(createdAt, chat.createdAt) && Objects.equals(updatedAt, chat.updatedAt);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, title, type, createdAt, updatedAt);
    }

    @Override
    public String toString() {
        return "Chat{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", type=" + type +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }

}
