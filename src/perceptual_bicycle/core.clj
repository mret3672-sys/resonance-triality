(ns perceptual-bicycle.core
  "Perceptual Bicycle: {0,1} + | + T(♾️) + A.

   T is an involution (T² = id) implemented as mirror-reverse with bracket swap.
   A (attention frame) is the steering map: hinge, chunk-size, start, and base.")

(require '[clojure.string :as str])

(def infinity "♾️")

(defn digits
  "Generate n digits on a ring of `base`, starting at `start`."
  [start n base]
  (map #(mod % base) (range start (+ start n))))

(defn chunked-str
  "Apply the | coupling operator every k items."
  [xs k]
  (->> xs
       (partition-all k)
       (map #(apply str %))
       (str/join "|")))

(defn T
  "Mirror/reverse transform with parenthesis swap.
   T is involutive on well-formed expressions produced in this namespace."
  [s]
  (-> s
      str/reverse
      (str/replace "(" "<tmp>")
      (str/replace ")" "(")
      (str/replace "<tmp>" ")")))

(defn build-palindromic
  "Generate a closed expression and enforce closure laws.

   A = {:hinge h :chunk-size k :start s :base b}
   - `hinge` counts the left-side digits as (inc hinge)
   - Remaining digits up to base-1 become the center run"
  [{:keys [hinge chunk-size start base]
    :or {chunk-size 3 start 0 base 10}}]
  (let [left-nums    (digits start (inc hinge) base)
        center-count (- base (inc hinge))
        center-nums  (digits (+ start (inc hinge)) center-count base)
        left         (str "(" (chunked-str left-nums chunk-size) ")")
        right        (T left)
        center-fwd   (apply str center-nums)
        center-rev   (apply str (reverse center-nums))
        full         (str left center-fwd infinity center-rev right)]
    (when-not (= right (T left))
      (throw (ex-info "right ≠ T(left)" {:left left :right right})))
    (when-not (= full (T full))
      (throw (ex-info "T(full) ≠ full" {:full full})))
    (when-not (= full (T (T full)))
      (throw (ex-info "T² ≠ id" {:full full})))
    {:full full
     :left left
     :right right
     :attention {:hinge hinge :chunk-size chunk-size :start start :base base}}))

(defn ride
  "Public steering API." 
  [attention-map]
  (build-palindromic attention-map))

(defn canonical-ride
  "Canonical foundational example in decimal, hinge at 6, chunk-size 3.
   => (012|345|6)789♾️987(6|543|210)"
  []
  (:full (ride {:hinge 6 :chunk-size 3 :start 0 :base 10})))
