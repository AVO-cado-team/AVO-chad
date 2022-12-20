package com.example.avochadbackend.repo;

import org.springframework.data.jpa.repository.JpaRepository;
import com.example.avochadbackend.models.Message;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MessageRepository extends JpaRepository<Message, Long> {
    List<Message> findByText(String text);
    List<Message> findByChatId(long id);

    
}
