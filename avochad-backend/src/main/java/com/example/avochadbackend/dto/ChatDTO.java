package com.example.avochadbackend.dto;

import java.util.List;

import com.example.avochadbackend.models.User;
import com.example.avochadbackend.utility.enums.ChatType;

public class ChatDTO {

    private String title;
    private ChatType type;
    private List<User> users;

    
    public ChatDTO() {
    }

    public ChatDTO(String title, ChatType type, List<User> users) {
        this.title = title;
        this.type = type;
        this.users = users;
    }

    public String getTitle() {
        return this.title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public ChatType getType() {
        return this.type;
    }

    public void setType(ChatType type) {
        this.type = type;
    }

    public List<User> getUsers() {
        return this.users;
    }

    public void setUsers(List<User> users) {
        this.users = users;
    }
}
