library(ggplot2)
f <- function(y, z) {
  pnorm(y + z) + 3* pnorm(y - z)
}
y_vals <- seq(-3, 3, length.out = 100)
z_vals <- seq(-3, 3, length.out = 100)
grid <- expand.grid(y = y_vals, z = z_vals)
grid$f_value <- with(grid, f(y, z))

point_data<-data.frame(
  x = c(-0.3, -0.9, -1.3, -2, 0.3, 0.9, 1.3, 2),
  y = -c(-0.3, -0.9, -1.3, -2, 0.3, 0.9, 1.3, 2)/2,
  shape = c(16, 17, 13, 15, 16, 17, 13, 15)
)

plot_1 = ggplot(grid, aes(x = y, y = z, z = f_value)) +
  geom_contour(bins=25,aes( colour = ..level..)) +
  scale_color_distiller(palette = "PuBu", direction = 1) +
  geom_segment(aes(x=-2.8,y=-2.8,xend=2.8,yend=2.8))+
  geom_point(data = point_data, aes(x = x, y = y, shape = as.factor(shape)),
             size=2.7,color="indianred4",inherit.aes = FALSE,
             show.legend = FALSE) + 
  #geom_path(data = point_data, aes(x = x, y = y), linetype = "dashed", color = "black", inherit.aes = FALSE)
  labs(
    x = "x",
    y = expression(x*"'"),
    title = expression(psi(x, x*"'") == Phi(x + x*"'") + 3*Phi(x - x*"'"))) +
  #theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5,size=16),
        axis.text = element_text(size=13),
        axis.title = element_text(size=13),
        legend.title = element_text(size=13),
        legend.text = element_text(size=13))

f <- function(y, z) {2*y-z}
y_vals <- seq(-3, 3, length.out = 100)
z_vals <- seq(-3, 3, length.out = 100)
grid <- expand.grid(y = y_vals, z = z_vals)
grid$f_value <- with(grid, f(y, z))

point_data<-data.frame(
  x = c(-0.5, -1, -1.5, -2, 0.5, 1, 1.5, 2),
  y = -c(-0.5, -1, -1.5, -2, 0.5, 1, 1.5, 2),
  shape = c(16, 17, 13, 15, 16, 17, 13, 15)
)

plot_2 = ggplot(grid, aes(x = y, y = z, z = f_value)) +
  geom_contour(bins=25,aes( colour = ..level..)) +
  scale_color_distiller(palette = "PuBu", direction = 1) +
  geom_segment(aes(x=-2.8,y=-2.8,xend=2.8,yend=2.8))+
  geom_point(data = point_data, aes(x = x, y = y, shape = factor(shape)),
             size=2.7,color="indianred4",inherit.aes = FALSE,
             show.legend = FALSE) + 
  labs(
    x = "x",
    y = expression(x*"'"),
    title = expression(psi(x, x*"'") == 2*x - x*"'")) +
  theme(plot.title = element_text(hjust = 0.5,size=16),
        axis.text = element_text(size=13),
        axis.title = element_text(size=13),
        legend.title = element_text(size=13),
        legend.text = element_text(size=13))

pdf(file = "figures/examples_of_psi.pdf",width = 13.5, height = 5)
gridExtra::grid.arrange(plot_1,plot_2,ncol=2)
dev.off()