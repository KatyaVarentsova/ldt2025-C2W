package hackaton.ldthackaton.service;

import hackaton.ldthackaton.client.MLServiceClient;
import hackaton.ldthackaton.dto.PredictionRequest;
import hackaton.ldthackaton.dto.PredictionResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PredictionService {

    @Autowired
    private MLServiceClient mlServiceClient;

    public PredictionResponse processReviews(PredictionRequest request) {
        // добавить логику предварительной обработки, возможно.
        // Пока просто передаем запрос ML-сервису и возвращаем его ответ.
        return mlServiceClient.getPredictions(request);
    }
}