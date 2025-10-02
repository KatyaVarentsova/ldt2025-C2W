package hackaton.ldthackaton.dto;

public class TotalTonalityDto {
    private Integer negative = 0;
    private Integer neutral = 0;
    private Integer positive = 0;

    // Геттеры
    public Integer getNegative() { return negative; }
    public Integer getNeutral() { return neutral; }
    public Integer getPositive() { return positive; }

    public void setNegative(Integer negative) { this.negative = negative; }
    public void setNeutral(Integer neutral) { this.neutral = neutral; }
    public void setPositive(Integer positive) { this.positive = positive; }
}