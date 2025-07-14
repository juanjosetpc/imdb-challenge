package com.imdb.system_module_2.mapper;

import com.imdb.system_module_2.dto.PersonDTO;
import com.imdb.system_module_2.entity.Person;

public class PersonMapper {
    public static PersonDTO toDTO(Person person) {
        PersonDTO dto = new PersonDTO();
        dto.setName(person.getPrimaryName());
        dto.setBirthYear(person.getBirthYear());
        dto.setDeathYear(person.getDeathYear());
        dto.setProfession(person.getPrimaryProfession());
        return dto;
    }
}
