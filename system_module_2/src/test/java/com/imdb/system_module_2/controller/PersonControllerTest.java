package com.imdb.system_module_2.controller;

import com.imdb.system_module_2.dto.PersonDTO;
import com.imdb.system_module_2.service.PersonService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockito.Mockito.when;

import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Collections;
import java.util.List;

@ExtendWith(MockitoExtension.class)
class PersonControllerTest {

    @InjectMocks
    private PersonController peopleController;

    @Mock
    private PersonService peopleService;

    @Test
    void shouldReturnBadRequestWhenNameIsNull() {
        ResponseEntity<?> response = peopleController.getPeopleByName(null);
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertEquals("The parameter 'name' is compulsory and cannot be empty.", response.getBody().toString().trim());
    }

    @Test
    void shouldReturnBadRequestWhenNameIsBlank() {
        ResponseEntity<?> response = peopleController.getPeopleByName("   ");
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void shouldReturnNoContentWhenPeopleListIsEmpty() {
        when(peopleService.findPeopleByName("john")).thenReturn(Collections.emptyList());

        ResponseEntity<?> response = peopleController.getPeopleByName("john");

        assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
        assertNull(response.getBody());
    }

    @Test
    void shouldReturnPeopleListWhenFound() {
        List<PersonDTO> people = List.of(new PersonDTO("John",1970, null, "actor"));
        when(peopleService.findPeopleByName("john")).thenReturn(people);

        ResponseEntity<?> response = peopleController.getPeopleByName("john");

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(people, response.getBody());
    }
}
