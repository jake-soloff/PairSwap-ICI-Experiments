library(ggplot2)

#define the data points
bin_1_data <- data.frame(
  z = seq(1, 3.5, 0.5),
  y = c(2.2, 0.8, -1.1, 3, -2.3, -1.0)
)
bin_1_data = bin_1_data[order(bin_1_data$y,decreasing = TRUE),]
bin_2_data <- data.frame(
  z = seq(4, 6.5, 0.5),
  y = c( -2.3, -1.0, 2.4, 1.2, 0.9,-3)
)
bin_2_data = bin_2_data[order(bin_2_data$y,decreasing = TRUE),]
bin_3_data <- data.frame(
  z = seq(7, 9.5, 0.5),
  y = c(-2.1, -0.8, 1.3, 2.0 , 0.4,-2.2)
)
bin_3_data = bin_3_data[order(bin_3_data$y,decreasing = TRUE),]
bin_4_data <- data.frame(
  z = seq(10, 12.5, 0.5),
  y = c(0.3,-2.5, -2.9, -0.5, -1.5,2.2)
)
bin_4_data = bin_4_data[order(bin_4_data$y,decreasing = TRUE),]


# compute medians
combined_data <- rbind(bin_1_data, bin_2_data, bin_3_data, bin_4_data)
median_bin_1 <- median(bin_1_data$y)
median_bin_2 <- median(bin_2_data$y)
median_bin_3 <- median(bin_3_data$y)
median_bin_4 <- median(bin_4_data$y)

#define matching
segments_data <- data.frame(
  x = c(bin_1_data[bin_1_data$y>median_bin_1,]$z,
        bin_2_data[bin_2_data$y>median_bin_2,]$z,
        bin_3_data[bin_3_data$y>median_bin_3,]$z),
  y = c(bin_1_data[bin_1_data$y>median_bin_1,]$y,
        bin_2_data[bin_2_data$y>median_bin_2,]$y,
        bin_3_data[bin_3_data$y>median_bin_3,]$y),
  xend = c(rev(bin_2_data[bin_2_data$y<median_bin_2,]$z),
           rev(bin_3_data[bin_3_data$y<median_bin_3,]$z),
           rev(bin_4_data[bin_4_data$y<median_bin_4,]$z)),
  yend = c(rev(bin_2_data[bin_2_data$y<median_bin_2,]$y),
           rev(bin_3_data[bin_3_data$y<median_bin_3,]$y),
           rev(bin_4_data[bin_4_data$y<median_bin_4,]$y))
)

#plot
p <- ggplot(combined_data, aes(x = z, y = y)) +
  geom_point(color = "black", shape = 16) + 
  geom_vline(xintercept = c(0.75, 3.75, 6.75, 9.75, 12.75), linetype = "solid", color = "black") +
  annotate("text", x = 2.25, y = max(combined_data$y) + 0.5, label = expression(A[1]), color = "black", size = 5) +
  annotate("text", x = 5.25, y = max(combined_data$y) + 0.5, label = expression(A[2]), color = "black", size = 5) +
  annotate("text", x = 8.25, y = max(combined_data$y) + 0.5, label = expression(A[3]), color = "black", size = 5) +
  annotate("text", x = 11.25, y = max(combined_data$y) + 0.5, label = expression(A[4]), color = "black", size = 5) +
  # Add median lines for each bin
  geom_segment(aes(x = 0.75, xend = 3.75, y = median_bin_1, yend = median_bin_1), color = "black", linetype = "dashed") +
  geom_segment(aes(x = 3.75, xend = 6.75, y = median_bin_2, yend = median_bin_2), color = "black", linetype = "dashed") +
  geom_segment(aes(x = 6.75, xend = 9.75, y = median_bin_3, yend = median_bin_3), color = "black", linetype = "dashed") +
  geom_segment(aes(x = 9.75, xend = 12.75, y = median_bin_4, yend = median_bin_4), color = "black", linetype = "dashed") +
  geom_segment(data = segments_data, aes(x = x, y = y, xend = xend, yend = yend), color = "skyblue", linetype = "solid") +
  labs( x = "Z", y = "Y") +
  theme_minimal()+ 
  theme(
    axis.text.x = element_blank(),
    axis.text.y = element_blank()
  )

pdf(file = "figures/cross_bin_demonstration.pdf",width = 4.5, height = 3.5)
p
dev.off()