\ProvidesClass{report}

\LoadClass{article}

% Microtypographic improvements
\RequirePackage{microtype}

% Concrete Math typefaces
%\RequirePackage{euler}
%\RequirePackage{beton}

% Linux Libertine typeface
\RequirePackage{fontspec}
\setmainfont[
  Ligatures=TeX
]{Linux Libertine O}

% AMS tools
\RequirePackage{amsmath}
\RequirePackage{amsthm}
\RequirePackage{amssymb}

% Number only referenced equations
\RequirePackage{autonum}

% Fancy tables & pretty tables
\RequirePackage{array}
\RequirePackage{xcolor}
\RequirePackage{colortbl}
\RequirePackage{longtable}
\RequirePackage{tabu}
\RequirePackage{booktabs}

% Customizable lists
\RequirePackage{paralist}

% Nice code listing
\RequirePackage{listings}

% Make references clever
\RequirePackage{varioref}
\RequirePackage{cleveref}

% Listings controls
\lstset{
  language=c,
  basicstyle=\ttfamily
}