use std::time::SystemTime;
const LESS: &'static str = "<";
const MORE: &'static str = ">";
const SAME: &'static str = " ";
const DIFF: &'static str = "|";

const STYLE_HTML: &'static str = "<style type=\"text/css\">
    table, th, td {
      border: 1px solid black;
    }
</style>";

#[derive(Debug)]
pub struct Line {
    left: String,
    right: String,
    separator: &'static str
}

impl Line {
    fn len(&self) -> usize {
        self.left.len() + self.right.len() + self.separator.len()
    }

    fn to_html(&self) -> String {
        let mut s = String::with_capacity(self.len() * 2);
        s.push_str(format!("\t\t<td>{}</td>\n", self.left).as_str());
        let color = match self.separator {
            DIFF => " bgcolor=\"yellow\"",
            MORE => " bgcolor=\"green\"",
            LESS => " bgcolor=\"red\"",
            _ => " bgcolor=\"white\""
        };
        s.push_str(format!("\t\t<td {}>{}</td>", color, self.right).as_str());
        s
    }
}


#[derive(Debug)]
pub struct Diff {
    result: Vec<Line>
}

impl Diff {
    pub fn to_html(&self) -> String {
        let mut s = String::with_capacity((self.result.len() * self.result[0].len()) * 2);
        s.push_str("<!DOCTYPE html>\n<html>\n<head>\n");
        s.push_str(STYLE_HTML);
        s.push_str("</head>\n<body>\n<table style=\"width:100%\">");
        for line in &self.result {
            s.push_str("\t<tr>");
            s.push_str(line.to_html().as_str());
            s.push_str("\t</tr>");
        }
        s.push_str("</body>\n</html>");
        s
    }
}

struct ResettableIterator<'a> {
    items: Vec<&'a str>,
    idx: usize
}

impl<'a> ResettableIterator<'a> {
    fn new(items: Vec<&'a str>) -> Self {
        ResettableIterator {
            items: items,
            idx: 0
        }
    }

    fn reset(&mut self, idx: usize) {
        self.idx = idx;
    }
}


impl<'a> Iterator for ResettableIterator<'a> {
    type Item = (usize, &'a str);

    fn next(&mut self) -> Option<Self::Item> {
        if self.idx >= self.items.len() {
            None
        }
        else {
            self.idx += 1;
            Some((self.idx - 1, self.items[self.idx - 1]))
        }
    }
}

pub fn diff(a: &String, b: &String) -> Diff {
    let now = SystemTime::now();
    let mut result: Vec<Line> = Vec::new();
    let mut iter1 = ResettableIterator::new(a.split("\n").collect());
    let mut iter2 = ResettableIterator::new(b.split("\n").collect());
    compare(
        &mut result,
        &mut iter1,
        &mut iter2
    );
    println!("compare {}", now.elapsed().unwrap().as_micros());
    Diff {result: result}
}

fn make_line(a: &str, b: &str, separator: &'static str) -> Line {
    Line{ left: a.to_string(), right: b.to_string(), separator: separator }
}

fn compare(resp: &mut Vec<Line>, iter1: &mut ResettableIterator, iter2: &mut ResettableIterator) {
    let mut c1 = iter1.next();
    let mut c2 = iter2.next();

    if (c1 == None) && (c2 == None) {
        return;
    }

    let mut a;
    let mut b;
    while (c1 != None) && (c2 != None) {
        a = c1.unwrap();
        b = c2.unwrap();
        if a.1 == b.1 {
            resp.push(make_line(a.1, b.1, SAME));
            c1 = iter1.next();
            c2 = iter2.next();
        } else {
            break;
        }
    }

    if (c1 != None) && (c2 != None) {
        a = c1.unwrap();
        b = c2.unwrap();
        let c1_idx = a.0;

        let rest = &iter1.items[c1_idx..];
        if let Some(idx) = &rest.iter().position(|&x| x == b.1) {
            let mut seen = 0;
            for v in rest {
                if seen >= *idx {
                    break
                }

                resp.push(make_line(v, "", LESS));
                seen += 1;
            }

            iter1.reset(c1_idx + *idx);
            iter2.reset(b.0);
            compare(resp, iter1, iter2);
            return
        }

        // Advance right side
        let c2_idx = b.0;
        let rest = &iter2.items[c2_idx..];
        if let Some(idx) = &rest.iter().position(|&x| x == a.1) {
            let mut seen = 0;
            for v in rest {
                if seen >= *idx {
                    break
                }

                resp.push(make_line("", v, MORE));
                seen += 1;
            }

            iter1.reset(a.0);
            iter2.reset(c2_idx + *idx);
            compare(resp, iter1, iter2);
            return
        }
    }

    if (c1 != None) && (c2 != None) {
        a = c1.unwrap();
        b = c2.unwrap();
        resp.push(make_line(a.1, b.1, DIFF));
        compare(resp, iter1, iter2);
    } else {
        while c1 != None {
            a = c1.unwrap();
            resp.push(make_line(a.1, "", LESS));
            c1 = iter1.next();
        }

        while c2 != None {
            b = c2.unwrap();
            resp.push(make_line("", b.1, MORE));
            c2 = iter2.next();
        }

        return;
    }
}
