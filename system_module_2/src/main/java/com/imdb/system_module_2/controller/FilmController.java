package com.imdb.system_module_2.controller;

import com.imdb.system_module_2.dto.FilmDTO;
import com.imdb.system_module_2.dto.PersonDTO;
import com.imdb.system_module_2.service.FilmService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/films")
public class FilmController {

    @Autowired
    protected FilmService filmService;

    public FilmController(FilmService filmService) {
        this.filmService = filmService;
    }

    @GetMapping("/search")
    public ResponseEntity<?> getFilmsByTitle(@RequestParam String title) {
        if (title == null || title.trim().isEmpty()) {
            return ResponseEntity.badRequest()
                    .body("The film 'title' is compulsory and cannot be empty.");
        }

        List<FilmDTO> films = filmService.findMoviesByTitle(title);
        if (films.isEmpty()) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.ok(films);


    }


}
