package hackaton.ldthackaton.controller;

import hackaton.ldthackaton.dto.PredictionRequest;
import hackaton.ldthackaton.dto.PredictionResponse;
import hackaton.ldthackaton.service.PredictionService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class PredictionController {

    @Autowired
    private PredictionService predictionService;

    @PostMapping("/predict")
    public ResponseEntity<PredictionResponse> predict(@Valid @RequestBody PredictionRequest request) {
        // Вызов сервиса для обработки
        PredictionResponse response = predictionService.processReviews(request);
        return ResponseEntity.ok(response);
    }

    // Health-check endpoint
    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("UP");
    }
}