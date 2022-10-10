use std::fmt;

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
pub enum Color{
    Red,
    Green,
    Blue,
    LightBlue,
    LightGreen,
    Purple,
    Fusia,
    Grey,
    Orange,
    Yellow,
    Pink,
    Teal,
}

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Color::Red => write!(f, "RE"),
            Color::Green => write!(f, "GR"),
            Color::Blue => write!(f, "BL"),
            Color::LightBlue => write!(f, "LB"),
            Color::LightGreen => write!(f, "LG"),
            Color::Purple => write!(f, "PU"),
            Color::Fusia => write!(f, "FU"),
            Color::Grey => write!(f, "GY"),
            Color::Orange => write!(f, "OR"),
            Color::Yellow => write!(f, "YE"),
            Color::Pink => write!(f, "PI"),
            Color::Teal => write!(f, "TE"),
        }
    }
}

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct ColorBox{
    pub color: Color,
    pub count: u32,
}

impl ColorBox {
    pub fn new(c: Color, i: u32) -> ColorBox {
        ColorBox{
            color: c,
            count: i,
        }
    }

    #[allow(dead_code)]
    pub fn dump(&self) -> String {
        let mut vals: Vec<String> = Vec::new();
        for _ in 0..self.count {
            vals.push(format!("|{}|\n", self.color));
        }
        vals.join("")
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_color_box() {
        let c = ColorBox::new(Color::Blue, 1);
        assert_eq!(1, c.count);
    }

    #[test]
    fn test_color_equal() {
        let c1 = Color::Blue;
        let c2 = Color::Blue;
        assert_eq!(c1, c2);
    }

    #[test]
    fn test_color_box_equality() {
        let c1 = ColorBox::new(Color::Blue, 1);
        let c2 = ColorBox::new(Color::Blue, 1);
        assert_eq!(c1, c2);

        let c2 = ColorBox::new(Color::Blue, 0);
        assert_ne!(c1, c2);

        let c2 = ColorBox::new(Color::Green, 1);
        assert_ne!(c1, c2);
    }

    #[test]
    fn test_dump() {
        let c1 = ColorBox::new(Color::Blue, 2);
        let s = c1.dump();
        assert_eq!(s, "|BL|\n|BL|\n")
    }
}
