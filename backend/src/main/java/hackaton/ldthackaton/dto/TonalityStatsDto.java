package hackaton.ldthackaton.dto;

public class TonalityStatsDto {
    private Integer year;
    private String month;
    private int monthNumber;
    private Integer negative = 0;
    private Integer neutral = 0;
    private Integer positive = 0;

    public int getMonthNumber() {
        return monthNumber;
    }

    public void setMonthNumber(int monthNumber) {
        this.monthNumber = monthNumber;
    }
    public Integer getYear() { return year; }
    public void setYear(Integer year) { this.year = year; }

    public String getMonth() { return month; }
    public void setMonth(String month) { this.month = month; }

    public Integer getNegative() { return negative; }
    public void setNegative(Integer negative) { this.negative = negative; }

    public Integer getNeutral() { return neutral; }
    public void setNeutral(Integer neutral) { this.neutral = neutral; }

    public Integer getPositive() { return positive; }
    public void setPositive(Integer positive) { this.positive = positive; }
}
