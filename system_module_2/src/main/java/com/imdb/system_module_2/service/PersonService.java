package com.imdb.system_module_2.service;

import com.imdb.system_module_2.dto.PersonDTO;
import com.imdb.system_module_2.entity.Person;
import com.imdb.system_module_2.mapper.PersonMapper;
import com.imdb.system_module_2.repository.PersonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class PersonService {
    @Autowired
    protected PersonRepository personRepository;

    protected PersonMapper personMapper;

    public List<PersonDTO> findPeopleByName(String name) {
        List<Person> people = personRepository.findByPrimaryNameContainingIgnoreCase(name);
        List<PersonDTO> result = new ArrayList<>();
        people.forEach(person -> result.add(personMapper.toDTO(person)));
        return result;
    }

}
