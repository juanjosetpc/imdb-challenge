package com.imdb.system_module_2;

import io.github.cdimascio.dotenv.Dotenv;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SystemModule2Application {

	public static void main(String[] args) {

		Dotenv dotenv = Dotenv.configure()
				.directory("./system_module_2")
				.ignoreIfMissing()
				.load();

		dotenv.entries().forEach(entry -> {
			System.setProperty(entry.getKey(), entry.getValue());
		});

		SpringApplication.run(SystemModule2Application.class, args);
	}

}
