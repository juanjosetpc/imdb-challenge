package com.imdb.system_module_2.repository;

import com.imdb.system_module_2.entity.Person;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface PersonRepository extends JpaRepository<Person, String> {
    List<Person> findByPrimaryNameContainingIgnoreCase(String name);
}
