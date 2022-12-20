package com.example.avochadbackend.services;

import java.util.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.example.avochadbackend.models.User;
import com.example.avochadbackend.repo.UserRepository;
import com.example.avochadbackend.utility.enums.Role;
import com.example.avochadbackend.utility.enums.Status;

@Service
public class RegistrationService {

    private UserRepository userRepository;
    private PasswordEncoder passwordEncoder;

    @Autowired
    public RegistrationService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    // registration logic
    public void registerUser(User user) {
        user.setCreatedAt(new Date());
        user.setUpdatedAt(new Date());
        user.setRole(Role.USER);
        user.setStatus(Status.ONLINE);
        user.setPassword(passwordEncoder.encode(user.getPassword()));

        userRepository.save(user);
    }
}
