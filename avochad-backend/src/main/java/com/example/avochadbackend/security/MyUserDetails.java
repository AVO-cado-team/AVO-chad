package com.example.avochadbackend.security;
import java.util.Collection;
import java.util.Collections;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import com.example.avochadbackend.models.User;
import com.example.avochadbackend.utility.enums.Role;

public class MyUserDetails implements UserDetails{

    private final User user;

    public MyUserDetails(User user) {
        this.user = user;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        if (this.user.getRole().equals(Role.ADMIN) )
            return Collections.singletonList(new SimpleGrantedAuthority("ROLE_ADMIN"));
            
        else if (this.user.getRole().equals(Role.USER) )
            return Collections.singletonList(new SimpleGrantedAuthority("ROLE_USER"));

        return Collections.singletonList(new SimpleGrantedAuthority("ROLE_ANONYMOUS"));
    }

    @Override
    public String getPassword() {
        return this.user.getPassword();
    }
    
    @Override
    public String getUsername() {
        return this.user.getUsername();
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }


    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }


    @Override
    public boolean isEnabled() {
        return true;
    }

    public User getUser() {
        return this.user;
    }


}
