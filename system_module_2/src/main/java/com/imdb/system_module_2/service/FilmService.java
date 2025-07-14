package com.imdb.system_module_2.service;

import com.imdb.system_module_2.dto.FilmDTO;
import com.imdb.system_module_2.entity.Film;
import com.imdb.system_module_2.mapper.FilmMapper;
import com.imdb.system_module_2.repository.FilmRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class FilmService {

    @Autowired
    protected FilmRepository filmRepository;
    protected FilmMapper filmMapper;

    public List<FilmDTO> findMoviesByTitle(String title) {
        List<Film> films = filmRepository.findByPrimaryTitleContainingIgnoreCaseAndTitleType(title, "movie");
        List<FilmDTO> result = new ArrayList<>();
        films.forEach(film -> result.add(filmMapper.toDTO(film)));
        return result;
    }


}
