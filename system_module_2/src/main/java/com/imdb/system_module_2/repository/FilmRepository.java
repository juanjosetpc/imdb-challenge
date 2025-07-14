package com.imdb.system_module_2.repository;

import com.imdb.system_module_2.entity.Film;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface FilmRepository extends JpaRepository<Film, String> {
    List<Film> findByPrimaryTitleContainingIgnoreCaseAndTitleType(String title, String titleType);
}
