package com.imdb.system_module_2.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.*;

import java.util.List;
import java.util.ArrayList;

import com.imdb.system_module_2.dto.PersonDTO;
import com.imdb.system_module_2.entity.Person;
import com.imdb.system_module_2.repository.PersonRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

public class PersonServiceTest {

    @Mock
    private PersonRepository personRepository;

    @InjectMocks
    private PersonService personService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void findPeopleByName_ReturnsDTOList() {
        Person person = new Person();
        person.setNconst("nm123");
        person.setPrimaryName("John Doe");

        List<Person> mockPeople = new ArrayList<>();
        mockPeople.add(person);

        when(personRepository.findByPrimaryNameContainingIgnoreCase("john")).thenReturn(mockPeople);

        List<PersonDTO> result = personService.findPeopleByName("john");

        assertThat(result).isNotNull();
        assertThat(result).hasSize(1);
        assertThat(result.get(0).getName()).isEqualTo("John Doe");

        verify(personRepository, times(1)).findByPrimaryNameContainingIgnoreCase("john");
    }

    @Test
    void findPeopleByName_ReturnsEmptyListIfNoneFound() {
        when(personRepository.findByPrimaryNameContainingIgnoreCase("unknown")).thenReturn(new ArrayList<>());

        List<PersonDTO> result = personService.findPeopleByName("unknown");

        assertThat(result).isNotNull();
        assertThat(result).isEmpty();

        verify(personRepository, times(1)).findByPrimaryNameContainingIgnoreCase("unknown");
    }
}
