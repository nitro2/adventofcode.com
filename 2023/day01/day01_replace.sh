perl -pe 'BEGIN { %h = (one => 1, two => 2, three => 3, four => 4, five => 5, six => 6, seven =>7, eight => 8, nine => 9);
              $re = join "|", sort { length $b <=> length $a } keys %h; }
          s/($re)/$h{$1}/g'
