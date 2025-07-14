package com.imdb.system_module_2.controller;

import com.imdb.system_module_2.dto.PersonDTO;
import com.imdb.system_module_2.service.PersonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/people")
public class PersonController {

    @Autowired
    protected PersonService personService;

    @GetMapping("/search")
    public ResponseEntity<?> getPeopleByName(@RequestParam(required = true) String name) {
        if (name == null || name.trim().isEmpty()) {
            return ResponseEntity.badRequest()
                    .body("The parameter 'name' is compulsory and cannot be empty.");
        }

        List<PersonDTO> people = personService.findPeopleByName(name);
        if (people.isEmpty()) {
            return ResponseEntity.noContent().build();
        }

        return ResponseEntity.ok(people);
    }
}