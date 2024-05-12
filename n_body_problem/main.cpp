#include <SFML/Graphics.hpp>
#include <vector>
#include <cmath>
#include <iostream>
#include <cstdlib>
#include <time.h>
class Planet {
    public:
        // 6.67430e-11;
        static constexpr float G = 1;
        sf::CircleShape circle;
        sf::Vector2f velocity;
        float mass;
        Planet(float radius, int x, int y, float mass, sf::Vector2f velocity){
            this->circle.setRadius(radius);
            this->circle.setOrigin(circle.getRadius(), circle.getRadius());
            this->circle.setFillColor(sf::Color::White);
            this->circle.setPosition(x, y);
            this->velocity = velocity;
            this->mass = mass;
        }
        void draw(sf::RenderWindow& window) {
            window.draw(this->circle);
        }
        static float distances(Planet& A, Planet& B){
            return (A.circle.getPosition().x - B.circle.getPosition().x) * (A.circle.getPosition().x - B.circle.getPosition().x) + 
            (A.circle.getPosition().y - B.circle.getPosition().y) * (A.circle.getPosition().y - B.circle.getPosition().y);
        }
        static void attract(Planet& A, Planet& B, float time){
            float accA = (G * B.mass) /  distances(A, B);
            A.velocity += accA * time * (B.circle.getPosition() - A.circle.getPosition());
            A.circle.move(A.velocity * time);
            float accB = (G * A.mass) /  distances(A, B);
            B.velocity += accB * time * (A.circle.getPosition() - B.circle.getPosition());
            B.circle.move(B.velocity * time);
        }

};
void generate_planets(std::vector<Planet>& set, int n){
    for(int i = 0; i < n; i++){
        Planet temp(5.f,  1000 + std::rand() % 500, 600 + std::rand() % 500, std::rand() % 100, sf::Vector2f(-5 + std::rand() % 10, -5 + std::rand() % 10));
        set.push_back(temp);
    }
}
int main() {
    std::srand(std::time(nullptr));

    std::vector<Planet> set; 
    sf::RenderWindow window(sf::VideoMode(2500, 1500), "n_body_problem");
    sf::View view(sf::FloatRect(0, 0, 2500, 1500));
    window.setView(view);
    window.setFramerateLimit(60);
    // Planet A(5.f, 700, 400, 7500, sf::Vector2f(5, 0));
    // Planet B(5.f, 50, 400, 10100, sf::Vector2f(0, 1));
    // Planet C(5.f, 400, 50, 15000, sf::Vector2f(0, 10));
    Planet D(5.f, 200, 300, 10, sf::Vector2f(0, sqrt(90)));
    Planet F(5.f, 300, 300, 9000, sf::Vector2f(0, 0)); 
    // set.push_back(A);
    // set.push_back(B);
    // set.push_back(C);
    set.push_back(D);
    set.push_back(F);
    generate_planets(set, 100);
    sf::Clock clock;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Left)) {
            view.move(-20.0f, 0);
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Right)) {
            view.move(20.0f, 0);
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up)) {
            view.move(0, -20.0f);
        }
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down)) {
            view.move(0, 20.0f);
        }
        window.setView(view);
        float deltaTime = clock.restart().asSeconds();
        for(int i = 0; i < set.size() - 1; i++){
            for(int j = i + 1; j < set.size(); j++){
                Planet::attract(set[i], set[j], deltaTime);
            }
        }
        window.clear();
        for(Planet i : set){
            i.draw(window);
        }
        window.display();
    }

    return 0;
}