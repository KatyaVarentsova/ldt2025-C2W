package hackaton.ldthackaton.client;


import hackaton.ldthackaton.dto.PredictionRequest;
import hackaton.ldthackaton.dto.PredictionResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class MLServiceClient {

    @Value("${ml.service.url:http://localhost:5000}") // URL ML-сервиса, надо заменить на нужную
    private String mlServiceUrl;

    private final RestTemplate restTemplate;

    public MLServiceClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public PredictionResponse getPredictions(PredictionRequest request) {
        String url = mlServiceUrl + "/ml/predict";
        // Выполняем POST-запрос к ML-сервису
        return restTemplate.postForObject(url, request, PredictionResponse.class);
    }
}